"""initial migration

Revision ID: 56012781da93
Revises: 
Create Date: 2024-12-09 21:14:53.973690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56012781da93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ciudad',
    sa.Column('id_ciudad', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id_ciudad')
    )
    op.create_table('usuario',
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('contraseña', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id_usuario'),
    sa.UniqueConstraint('email')
    )
    op.create_table('evento',
    sa.Column('id_evento', sa.Integer(), nullable=False),
    sa.Column('nombre_evento', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('imagen', sa.String(length=200), nullable=True),
    sa.Column('id_ciudad', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ciudad'], ['ciudad.id_ciudad'], ),
    sa.PrimaryKeyConstraint('id_evento')
    )
    op.create_table('entrada',
    sa.Column('id_entrada', sa.Integer(), nullable=False),
    sa.Column('id_evento', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('fecha_compra', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_evento'], ['evento.id_evento'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id_usuario'], ),
    sa.PrimaryKeyConstraint('id_entrada')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entrada')
    op.drop_table('evento')
    op.drop_table('usuario')
    op.drop_table('ciudad')
    # ### end Alembic commands ###
