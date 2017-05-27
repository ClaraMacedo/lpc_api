from tastypie.resources import ModelResource
from tastypie import fields, utils
from tastypie.authorization import Authorization
from evento.models import *
from django.contrib.auth.models import User
from tastypie.exceptions import Unauthorized

#ok
class PessoaResource(ModelResource):
    class Meta:
        queryset = Pessoa.objects.all()
        allowed_methods = ['get','post','delete','put']
        authorization=Authorization()
        resource_name = 'pessoa'
        filtering = {
            "nome": ('exact', 'startswith',)
        }
#ok
class EventoResource(ModelResource):
    realizador= fields.ToOneField(PessoaResource, 'realizador')
    class Meta:
        queryset = Evento.objects.all()
        allowed_methods = ['get','post','delete','put']
        authorization=Authorization()
        filtering = {
            "nome": ('exact', 'startswith',)
            }
#ok
class EventoCientificoResource(ModelResource):
    realizador= fields.ToOneField(PessoaResource, 'realizador')
    class Meta:
        queryset = EventoCientifico.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'eventocientifico'
        authorization=Authorization()
        filtering = {
            "issn": ('exact', 'startswith',)
        }
#ok
class PessoaFisicaResource(ModelResource):
    class Meta:
        queryset = PessoaFisica.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'pessoafisica'
        authorization=Authorization()
        filtering = {
            "cpf": ('exact', 'startswith',)
        }
#ok
class PessoaJuridicaResource(ModelResource):
    class Meta:
        queryset = PessoaJuridica.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'pessoajuridica'
        authorization=Authorization()
        filtering = {
            "cnpj": ('exact', 'startswith',)
        }
#ok
class AutorResource(ModelResource):
    class Meta:
        queryset = Autor.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'autor'
        authorization=Authorization()
        filtering = {
            "curriculo": ('exact', 'startswith',)
        }

class ArtigoCientificoResource(ModelResource):
    evento = fields.ToOneField(EventoCientificoResource, 'evento')
    class Meta:
        queryset = ArtigoCientifico.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'artigocientifico'
        authorization=Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }####

class ArtigoAutorResource(ModelResource):
    autor = fields.ToOneField(AutorResource, 'autor')
    artigocientifico = fields.ToOneField(ArtigoCientificoResource, 'artigocientifico')
    class Meta:
        queryset = ArtigoAutor.objects.all()
        allowed_methods = ['get','post','delete','put']
        resource_name = 'artigoautor'
        authorization=Authorization()
        filtering = {
            "autor": ('exact', 'startswith',)
        }

class TipoInscricaoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        if not(TipoInscricao.objects.filter(descricao=bundle.data['descricao'].upper())):
            print(bundle.data)
            #print(kwargs)
            tipo=TipoInscricao()
            tipo.descricao= bundle.data['descricao'].upper()
            tipo.save()
            bundle.obj= tipo
        else:
            raise Unauthorized('Já existe tipo com este nome')
        #print(a)
        #if(len(a)>0):s
        #    print("jah existe")
        #    return False
        #else:
        #    return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized('Não pode-se apagar lista completa!')
        #exceptions

    class Meta:
        queryset = TipoInscricao.objects.all()
        allowed_methods = ['get','post','delete','put']
        authorization=Authorization()
        filtering = {
            "descricao": ('exact', 'startswith',)
            #tupla, palavra exata e começa com
        }


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']

class InscricaoResource(ModelResource):
    pessoa = fields.ToOneField(PessoaFisicaResource, 'pessoa')
    evento = fields.ToOneField(EventoResource, 'evento')
    def obj_create(self, bundle, **kwargs):
        #print(bundle.data['evento'])
        eventoPk=bundle.data['evento'].split('/')
        pessoaPk=bundle.data['pessoa'].split('/')
        #print(eventoPk[4])
        #print(pessoaPk[4])
        pes= Evento.pessoa
        if(Inscricoes.objects.filter(pessoa=pessoaPk)):
            print(eventoPk[4])

        if not(Inscricoes.objects.filter(pk=pessoaPk) and Inscricoes.objects.filter(evento=eventoPk)):
            print(eventoPk[4])
            #print(kwargs)
            tipo=Inscricoes()
            tipo.pessoafisica= bundle.data['pessoa']
            tipo.evento= bundle.data['evento']
            tipo.save()
            bundle.obj= tipo

        else:
            raise Unauthorized('Esta pessoa já esta inscrita neste evento')

    class Meta:
        queryset = Inscricoes.objects.all()
        allowed_methods = ['get','post','delete','put']
        authorization=Authorization()
        filtering = {
            "descricao": ('exact', 'startswith',)
            }
