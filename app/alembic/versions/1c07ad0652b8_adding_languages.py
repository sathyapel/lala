"""adding languages

Revision ID: 1c07ad0652b8
Revises: 43e6d788ae5f
Create Date: 2023-10-27 15:46:23.393506

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1c07ad0652b8'
down_revision = '43e6d788ae5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('languages', sa.Column('lang_code', sa.String(length=40), nullable=True))
    op.drop_column('languages', 'code')
    op.create_foreign_key(None, 'stories', 'languages', ['language'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stories', type_='foreignkey')
    op.add_column('languages', sa.Column('code', mysql.VARCHAR(length=30), nullable=False))
    op.drop_column('languages', 'lang_code')

    # ### end Alembic commands ###
