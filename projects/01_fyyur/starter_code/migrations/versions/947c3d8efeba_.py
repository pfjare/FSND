"""empty message

Revision ID: 947c3d8efeba
Revises: 2ac603d7e55f
Create Date: 2020-04-10 10:45:51.392132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947c3d8efeba'
down_revision = '2ac603d7e55f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artist', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)
    op.alter_column('artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('artist', 'website',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=False))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=300), nullable=False))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=False))
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=False))
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('venue', 'website')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'genres')
    op.alter_column('artist', 'website',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('artist', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    op.alter_column('artist', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###