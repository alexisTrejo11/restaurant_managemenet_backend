from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    
    def ready(self):
        """Se ejecuta cuando Django está completamente cargado"""
        from .injector.di_config import configure_di
        print("🔧 Inyectando dependencias...")
        configure_di()
        print("✅ Dependencias inyectadas correctamente")
        
       