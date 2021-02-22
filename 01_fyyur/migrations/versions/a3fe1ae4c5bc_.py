"""empty message

Revision ID: a3fe1ae4c5bc
Revises: 683a642dbddb
Create Date: 2021-02-20 13:34:18.601707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3fe1ae4c5bc'
down_revision = '683a642dbddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('artists', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'website')
    op.drop_column('artists', 'seeking_talent')
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###