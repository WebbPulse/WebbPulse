from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from slugify import slugify
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import Category, Post, User
from ....schemas import Category as CategorySchema
from ....schemas import CategoryCreate, CategoryUpdate
from ....schemas import Post as PostSchema
from ....schemas import PostCreate, PostList, PostUpdate

router = APIRouter()


@router.get("/", response_model=List[PostList])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_slug: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all published posts with pagination and optional category filter"""
    query = db.query(Post).filter(Post.published_at.isnot(None))

    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)

    posts = query.order_by(Post.published_at.desc()).offset(skip).limit(limit).all()
    return posts


@router.get("/admin", response_model=List[PostSchema])
async def get_all_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all posts (including unpublished) for admin panel"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view all posts")

    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return posts


# Category management endpoints (since categories are specific to blog posts)
@router.get("/categories", response_model=List[CategorySchema])
async def get_categories(db: Session = Depends(get_db)):
    """Get all blog post categories"""
    categories = db.query(Category).order_by(Category.name).all()
    return categories


@router.get("/{slug}", response_model=PostSchema)
async def get_post(slug: str, db: Session = Depends(get_db)):
    """Get a single post by slug"""
    post = (
        db.query(Post).filter(Post.slug == slug, Post.published_at.isnot(None)).first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/category/{category_slug}", response_model=List[PostList])
async def get_posts_by_category(
    category_slug: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get posts by category slug"""
    posts = (
        db.query(Post)
        .join(Category)
        .filter(Category.slug == category_slug, Post.published_at.isnot(None))
        .order_by(Post.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


# Admin-only post management endpoints
@router.post("/admin", response_model=PostSchema)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new blog post (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create posts")

    # Generate slug if not provided
    if not post.slug:
        post.slug = slugify(post.title)

    # Check if slug already exists
    existing_post = db.query(Post).filter(Post.slug == post.slug).first()
    if existing_post:
        raise HTTPException(
            status_code=400, detail="Post with this slug already exists"
        )

    # Validate category exists if provided
    if post.category_id:
        from app.models.category import Category

        category = db.query(Category).filter(Category.id == post.category_id).first()
        if not category:
            raise HTTPException(status_code=422, detail="Category not found")

    db_post = Post(
        title=post.title,
        slug=post.slug,
        content=post.content,
        excerpt=post.excerpt,
        read_time=post.read_time,
        category_id=post.category_id,
        author_id=current_user.id,
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.put("/admin/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a blog post (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update posts")

    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update fields
    for field, value in post_update.model_dump(exclude_unset=True).items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)

    return db_post


@router.delete("/admin/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a blog post (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete posts")

    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()

    return {"message": "Post deleted successfully"}


@router.post("/admin/{post_id}/publish")
async def publish_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Publish a blog post (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to publish posts")

    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.published_at:
        raise HTTPException(status_code=400, detail="Post is already published")

    db_post.published_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Post published successfully"}


@router.post("/categories", response_model=CategorySchema)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new blog post category (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to create categories"
        )

    # Generate slug if not provided
    if not category.slug:
        category.slug = slugify(category.name)

    # Check if slug already exists
    existing_category = (
        db.query(Category).filter(Category.slug == category.slug).first()
    )
    if existing_category:
        raise HTTPException(
            status_code=400, detail="Category with this slug already exists"
        )

    db_category = Category(name=category.name, slug=category.slug)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@router.put("/categories/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a blog post category (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update categories"
        )

    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Update fields
    for field, value in category_update.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)

    db.commit()
    db.refresh(db_category)

    return db_category


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a blog post category (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete categories"
        )

    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category has posts
    if db_category.posts:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete category that has posts. "
                "Please reassign or delete the posts first."
            ),
        )

    db.delete(db_category)
    db.commit()

    return {"message": "Category deleted successfully"}
