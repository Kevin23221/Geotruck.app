def es_admin(user):
    return user.groups.filter(name="administrador").exists()


def es_supervisor(user):
    return user.groups.filter(name="supervisor").exists()


def es_conductor(user):
    return user.groups.filter(name="conductor").exists()