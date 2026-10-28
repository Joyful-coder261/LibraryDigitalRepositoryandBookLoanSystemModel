"""Import every model so SQLAlchemy and Alembic register all 25 tables."""
from app.models.access_control import Role, Permission, UserRole, RolePermission
from app.models.user import User
from app.models.catalogue import (
    Resource, Author, ResourceAuthor, Category, ResourceCategory
)
from app.models.digital_repository import DigitalAsset
from app.models.inventory import PhysicalCopy
from app.models.circulation import Loan, Reservation
from app.models.intelligence import (
    Topic, ResourceTopic, UserInteraction, UserInterest, Recommendation, KnowledgeLink
)
from app.models.notifications import Notification, NotificationPreference, NotificationDelivery
from app.models.audit import AuditLog, LoginEvent

__all__ = [
    "Role", "Permission", "UserRole", "RolePermission", "User",
    "Resource", "Author", "ResourceAuthor", "Category", "ResourceCategory",
    "Topic", "ResourceTopic", "PhysicalCopy", "DigitalAsset", "Loan", "Reservation",
    "UserInteraction", "UserInterest", "Recommendation", "KnowledgeLink",
    "Notification", "NotificationPreference", "NotificationDelivery",
    "AuditLog", "LoginEvent",
]
