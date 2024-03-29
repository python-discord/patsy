"""
${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
import sqlalchemy as sa
from alembic import op

${imports if imports else ""}
#  Revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Apply this migration."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Revert this migration."""
    ${downgrades if downgrades else "pass"}
