# ---------------------------------------------------------------------------
# VPC — two public subnets (2 AZs for RDS subnet group requirement).
#
# RDS is publicly accessible but secured by:
#   - 32-char alphanumeric password (random_password.db, ~190 bits entropy)
#   - PostgreSQL native auth
#   - rds.force_ssl = 1 on the DB parameter group (SSL required)
#
# App Runner uses default (AWS-managed) egress — no VPC connector, no NAT.
# ---------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = local.prefix }
}

# RDS subnet groups require subnets in at least two AZs.
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = { Name = "${local.prefix}-public-a" }
}

# New CIDR (not 10.0.2.0/24, which belonged to private_b) so terraform can
# create this before destroying private_b without a range collision.
resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = { Name = "${local.prefix}-public-b" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = { Name = local.prefix }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = { Name = "${local.prefix}-public" }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

# App Runner egress IPs are AWS-managed and not fixed, so 0.0.0.0/0 is
# required on the ingress rule. DB auth + rds.force_ssl secure the instance.
resource "aws_security_group" "rds" {
  name        = "${local.prefix}-rds"
  description = "Allow PostgreSQL inbound (secured by auth + SSL)"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${local.prefix}-rds" }
}
