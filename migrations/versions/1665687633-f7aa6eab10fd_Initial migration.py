"""
Initial migration.

Revision ID: f7aa6eab10fd
Revises:
Create Date: 2022-10-13 19:00:33.969508+00:00
"""
import sqlalchemy as sa
from alembic import op

#  Revision identifiers, used by Alembic.
revision = 'f7aa6eab10fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply this migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('opted_out', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('user_id', name=op.f('users_pk'))
    )
    op.create_table(
        'help_sessions',
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('claimant_id', sa.Integer(), nullable=True),
        sa.Column('channel_id', sa.BigInteger(), nullable=True),
        sa.Column('opened_at', sa.DateTime(), nullable=True),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['claimant_id'], ['users.user_id'], name=op.f('help_sessions_claimant_id_users_fk')),
        sa.PrimaryKeyConstraint('session_id', name=op.f('help_sessions_pk'))
    )
    op.create_table(
        'messages',
        sa.Column('message_id', sa.BigInteger(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('session_id', sa.Integer(), nullable=True),
        sa.Column('channel_id', sa.BigInteger(), nullable=True),
        sa.Column('content', sa.String(length=4000), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], name=op.f('messages_author_id_users_fk')),
        sa.ForeignKeyConstraint(
            ['session_id'],
            ['help_sessions.session_id'],
            name=op.f('messages_session_id_help_sessions_fk')
        ),
        sa.PrimaryKeyConstraint('message_id', name=op.f('messages_pk'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Revert this migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('help_sessions')
    op.drop_table('users')
    # ### end Alembic commands ###