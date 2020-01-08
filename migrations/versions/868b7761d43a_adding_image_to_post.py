"""adding image to post

Revision ID: 868b7761d43a
Revises: 70b383bd8262
Create Date: 2020-01-07 20:19:46.480519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868b7761d43a'
down_revision = '70b383bd8262'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image')
    # ### end Alembic commands ###