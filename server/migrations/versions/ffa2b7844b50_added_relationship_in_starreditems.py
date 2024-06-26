from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffa2b7844b50'
down_revision = '467b92a51617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starred_items', schema=None) as batch_op:
        batch_op.drop_constraint('fk_starred_items_folder_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_starred_items_user_id', 'users', ['user_id'], ['id'])
        batch_op.drop_column('folder_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starred_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('folder_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('fk_starred_items_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_starred_items_folder_id', 'folders', ['folder_id'], ['id'])

    # ### end Alembic commands ###
