"""Add tables to db

Revision ID: fd934a83bf40
Revises: 
Create Date: 2023-07-05 16:35:58.759267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd934a83bf40'
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