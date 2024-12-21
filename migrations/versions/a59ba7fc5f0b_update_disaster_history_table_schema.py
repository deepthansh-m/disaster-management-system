"""Update disaster_history table schema

Revision ID: a59ba7fc5f0b
Revises: 425cf44c24d4
Create Date: 2024-12-09 17:14:59.144752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59ba7fc5f0b'
down_revision = '425cf44c24d4'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the old table if it exists
    op.drop_table('disaster_history')

    # Create the new table based on your updated schema
    op.create_table(
        'disaster_history',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('disaster_type', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('rainfall', sa.Float(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('disaster_occurred', sa.Boolean(), nullable=False, default=False),
    )

def downgrade():
    # Drop the new table and revert to the old table (if necessary)
    op.drop_table('disaster_history')

    # You can recreate the old table if required
    op.create_table(
        'disaster_history',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('disaster_type', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
    )
