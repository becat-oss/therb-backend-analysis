"""empty message

Revision ID: f5a36f80d21b
Revises: 6580dfed064f
Create Date: 2022-09-01 13:00:14.693635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a36f80d21b'
down_revision = '6580dfed064f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('therb', sa.Column('sensibleHeat', sa.JSON(), nullable=True))
    op.add_column('therb', sa.Column('latentHeat', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('therb', 'latentHeat')
    op.drop_column('therb', 'sensibleHeat')
    # ### end Alembic commands ###