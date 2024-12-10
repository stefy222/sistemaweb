"""Agregar columna categoria a Evento

Revision ID: 90885d773db8
Revises: 56012781da93
Create Date: 2024-12-09 22:52:07.303481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90885d773db8'
down_revision = '56012781da93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('evento', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('evento', schema=None) as batch_op:
        batch_op.drop_column('categoria')

    # ### end Alembic commands ###