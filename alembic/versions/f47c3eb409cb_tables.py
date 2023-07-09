"""tables

Revision ID: f47c3eb409cb
Revises: 
Create Date: 2023-07-05 09:29:23.304601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f47c3eb409cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('professionals', sa.Column('phone_no', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('professionals', 'phone_no')
    # ### end Alembic commands ###
