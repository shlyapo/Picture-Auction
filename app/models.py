Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    login = Column(Text(), )
    password = Column(Text())
    name_user = Column(Text())
    surname = Column(Text())
    role = Column(Boolean(), default=False)
    admins = relationship("Admin", backref="user")
    owners = relationship("Owner", backref="user")
    authors = relationship("Author", backref="user")
    reviewers = relationship("Reviewer", backref="user")
    actionners = relationship("Actionner", backref="user")
    applications = relationship("Application", backref="user")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )


class Admin(Base):
    __tablename__ = 'administrators'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    __table_args__ = (
        PrimaryKeyConstraint('id', name='administrators_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Owner(Base):
    __tablename__='owners'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForegnKey("users.id"))

    def __repr__(self):
        return '<User %r>' % (self.nickname)