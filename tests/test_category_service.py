from app import db
from app.models import Category
from app.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
from app.services.category_service import CategoryService


class DummyForm(dict):
    def get(self, key, default=None):
        return super().get(key, default)


# Helpers

def build_category_form(name="Work", description="Google accounts", **overrides) -> DummyForm:
    data = {"name": name, "description": description}
    data.update(overrides)
    return DummyForm(**data)


def make_category_service() -> CategoryService:
    return CategoryService(categories=SqlAlchemyCategoryRepository(db))


def create_category_in_db(app, name="Work", description="Google accounts") -> int:
    with app.app_context():
        cat = Category(name=name, description=description)
        db.session.add(cat)
        db.session.commit()
        return cat.id


# Category tests

def test_list_categories_returns_sorted_by_name(app):
    with app.app_context():
        db.session.add_all(
            [
                Category(name="Zeta", description=""),
                Category(name="Alpha", description=""),
            ]
        )
        db.session.commit()

        service = make_category_service()
        cats = service.list_categories()

        assert [c.name for c in cats] == ["Alpha", "Zeta"]


def test_create_category_success(app):
    with app.app_context():
        service = make_category_service()
        cat, errors, _ = service.create_category(
            build_category_form(name="Work", description="Google accounts")
        )

        assert errors == []
        assert cat is not None
        assert cat.name == "Work"
        assert cat.description == "Google accounts"

        saved = Category.query.filter_by(name="Work").first()
        assert saved is not None


def test_create_category_validation_error(app):
    with app.app_context():
        service = make_category_service()
        cat, errors, _ = service.create_category(build_category_form(name=""))

        assert cat is None
        assert "Name is required." in errors


def test_create_category_duplicate_name_returns_error(app):
    create_category_in_db(app, name="Work", description="Google accounts")

    with app.app_context():
        service = make_category_service()
        cat, errors, _ = service.create_category(
            build_category_form(name="Work", description="Duplicate")
        )

        assert cat is None
        assert "A category with that name already exists." in errors


def test_update_category_success(app):
    cat_id = create_category_in_db(app, name="Work", description="Google accounts")

    with app.app_context():
        service = make_category_service()
        cat = db.session.get(Category, cat_id)

        errors, _ = service.update_category(
            cat,
            build_category_form(name="Work Updated", description="Google accounts updated"),
        )

        assert errors == []
        refreshed = db.session.get(Category, cat_id)
        assert refreshed.name == "Work Updated"
        assert refreshed.description == "Google accounts updated"


def test_update_category_validation_error(app):
    cat_id = create_category_in_db(app, name="Work", description="Google accounts")

    with app.app_context():
        service = make_category_service()
        cat = db.session.get(Category, cat_id)

        errors, _ = service.update_category(cat, build_category_form(name=""))

        assert "Name is required." in errors


def test_update_category_duplicate_name_returns_error(app):
    create_category_in_db(app, name="Work", description="Google accounts")
    cat2_id = create_category_in_db(app, name="Personal", description="Google accounts")

    with app.app_context():
        service = make_category_service()
        cat2 = db.session.get(Category, cat2_id)

        errors, _ = service.update_category(
            cat2,
            build_category_form(name="Work", description="Trying to duplicate name"),
        )

        assert "A category with that name already exists." in errors

        refreshed = db.session.get(Category, cat2_id)
        assert refreshed.name == "Personal"


def test_delete_category_removes_from_db(app):
    cat_id = create_category_in_db(app, name="Work", description="Google accounts")

    with app.app_context():
        service = make_category_service()
        cat = db.session.get(Category, cat_id)

        service.delete_category(cat)

        assert db.session.get(Category, cat_id) is None