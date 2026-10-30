
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


class UsuarioAutenticadoMixin(LoginRequiredMixin):
    login_url = 'login'


class AdultoResponsableMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
):
    login_url = 'login'

    def test_func(self):
        usuario = self.request.user

        return (
            usuario.is_superuser
            or usuario.groups.filter(
                name='Adultos responsables'
            ).exists()
        )
