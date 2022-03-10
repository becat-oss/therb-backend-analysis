"""initialized

Revision ID: 8c63c7cd3247
Revises: 
Create Date: 2021-09-25 09:06:29.883803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c63c7cd3247'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hour', sa.JSON(), nullable=False),
    sa.Column('roomT', sa.JSON(), nullable=False),
    sa.Column('clodS', sa.JSON(), nullable=False),
    sa.Column('rhexS', sa.JSON(), nullable=False),
    sa.Column('ahexS', sa.JSON(), nullable=False),
    sa.Column('fs', sa.JSON(), nullable=False),
    sa.Column('roomH', sa.JSON(), nullable=False),
    sa.Column('clodL', sa.JSON(), nullable=False),
    sa.Column('rhexL', sa.JSON(), nullable=False),
    sa.Column('ahexL', sa.JSON(), nullable=False),
    sa.Column('fl', sa.JSON(), nullable=False),
    sa.Column('mrt', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('project')
    # ### end Alembic commands ###