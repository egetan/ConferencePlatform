"""Initial migration.

Revision ID: 3c67e2a5205d
Revises: 
Create Date: 2020-11-27 00:20:56.486593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3c67e2a5205d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ConferenceRoles',
    sa.Column('ConfID', sa.Integer(), nullable=False),
    sa.Column('AuthenticationID', sa.Integer(), nullable=False),
    sa.Column('Role', sa.Enum(name='cnf_role'), nullable=True),
    sa.ForeignKeyConstraint(['AuthenticationID'], ['Users.AuthenticationID'], ),
    sa.ForeignKeyConstraint(['ConfID'], ['Conferences.ConfID'], ),
    sa.PrimaryKeyConstraint('ConfID', 'AuthenticationID')
    )
    op.drop_table('ConfrenceRoles')
    op.alter_column('City', 'CityName',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_constraint('city_country_countrycode_fk', 'City', type_='foreignkey')
    op.create_foreign_key(None, 'City', 'Country', ['CountryCode'], ['CountryCode'])
    op.drop_constraint('conferencetags_conferences_confid_fk', 'ConferenceTags', type_='foreignkey')
    op.create_foreign_key(None, 'ConferenceTags', 'Conferences', ['ConfID'], ['ConfID'])
    op.add_column('Conferences', sa.Column('SubmissionDeadline', sa.Date(), nullable=True))
    op.add_column('Conferences', sa.Column('WebSite', sa.VARCHAR(length=100), nullable=True))
    op.alter_column('Conferences', 'CreationDateTime',
               existing_type=postgresql.TIME(),
               nullable=True)
    op.alter_column('Conferences', 'CreatorUser',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Conferences', 'EndDate',
               existing_type=postgresql.TIME(),
               nullable=True)
    op.alter_column('Conferences', 'Name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('Conferences', 'ShortName',
               existing_type=sa.VARCHAR(length=19),
               nullable=True)
    op.alter_column('Conferences', 'StartDate',
               existing_type=postgresql.TIME(),
               nullable=True)
    op.alter_column('Conferences', 'Year',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'Conferences', 'UsersInfo', ['CreatorUser'], ['AuthenticationID'])
    op.drop_column('Conferences', 'SubmissionDeadLine')
    op.drop_column('Conferences', 'Website')
    op.alter_column('Country', 'CountryName',
               existing_type=sa.CHAR(length=50),
               nullable=True)
    op.alter_column('UserLog', 'Address',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('UserLog', 'Affiliation',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('UserLog', 'City',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('UserLog', 'Country',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('UserLog', 'LastName',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('UserLog', 'Name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('UserLog', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('UserLog', 'Phone',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('UserLog', 'PrimaryEmail',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('UserLog', 'RecordCreationDate',
               existing_type=postgresql.TIME(),
               nullable=True)
    op.alter_column('UserLog', 'Salutation',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('Users', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('Users', 'Username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.drop_index('users_username_uindex', table_name='Users')
    op.drop_constraint('users_users_info_authenticationid_fk', 'Users', type_='foreignkey')
    op.create_foreign_key(None, 'Users', 'UsersInfo', ['AuthenticationID'], ['AuthenticationID'])
    op.alter_column('UsersInfo', 'Affiliation',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('UsersInfo', 'LastName',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('UsersInfo', 'Name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('UsersInfo', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('UsersInfo', 'PrimaryEmail',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('UsersInfo', 'RecordCreationDate',
               existing_type=postgresql.TIME(),
               nullable=True)
    op.alter_column('UsersInfo', 'Salutation',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('UsersInfo', 'Salutation',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UsersInfo', 'RecordCreationDate',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.alter_column('UsersInfo', 'PrimaryEmail',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UsersInfo', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UsersInfo', 'Name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('UsersInfo', 'LastName',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('UsersInfo', 'Affiliation',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_constraint(None, 'Users', type_='foreignkey')
    op.create_foreign_key('users_users_info_authenticationid_fk', 'Users', 'UsersInfo', ['AuthenticationID'], ['AuthenticationID'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_index('users_username_uindex', 'Users', ['Username'], unique=True)
    op.alter_column('Users', 'Username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('Users', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UserLog', 'Salutation',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UserLog', 'RecordCreationDate',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.alter_column('UserLog', 'PrimaryEmail',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UserLog', 'Phone',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('UserLog', 'Password',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UserLog', 'Name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('UserLog', 'LastName',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('UserLog', 'Country',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('UserLog', 'City',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('UserLog', 'Affiliation',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('UserLog', 'Address',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('Country', 'CountryName',
               existing_type=sa.CHAR(length=50),
               nullable=False)
    op.add_column('Conferences', sa.Column('Website', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('Conferences', sa.Column('SubmissionDeadLine', postgresql.TIME(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Conferences', type_='foreignkey')
    op.alter_column('Conferences', 'Year',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Conferences', 'StartDate',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.alter_column('Conferences', 'ShortName',
               existing_type=sa.VARCHAR(length=19),
               nullable=False)
    op.alter_column('Conferences', 'Name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('Conferences', 'EndDate',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.alter_column('Conferences', 'CreatorUser',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Conferences', 'CreationDateTime',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.drop_column('Conferences', 'WebSite')
    op.drop_column('Conferences', 'SubmissionDeadline')
    op.drop_constraint(None, 'ConferenceTags', type_='foreignkey')
    op.create_foreign_key('conferencetags_conferences_confid_fk', 'ConferenceTags', 'Conferences', ['ConfID'], ['ConfID'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'City', type_='foreignkey')
    op.create_foreign_key('city_country_countrycode_fk', 'City', 'Country', ['CountryCode'], ['CountryCode'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column('City', 'CityName',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.create_table('ConfrenceRoles',
    sa.Column('ConfID', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('AuthenticationID', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Role', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['AuthenticationID'], ['UsersInfo.AuthenticationID'], name='confrencetags_users_info_authenticationid_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ConfID'], ['Conferences.ConfID'], name='confrencetags_conferences_confid_fk', onupdate='CASCADE', ondelete='CASCADE')
    )
    op.drop_table('ConferenceRoles')
    # ### end Alembic commands ###
