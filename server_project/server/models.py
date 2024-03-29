import datetime
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Chief(User):
    USERS_ROLES = [
        ('project_program_both_chief', 'Jefe de Proyecto/ Programa'),
        ('human_resources', 'Recursos Humanos'),
        ('economy', 'Economia'),
        ('vicedec_inv_postgr', 'Vicedecano de Investigacion y Postgrado')

    ]
    chief_type = models.TextField(max_length=255, choices=USERS_ROLES, default='human_resources')
    c_id = models.CharField(max_length=11, null=True, blank=True)

    faculty = models.CharField(max_length=20, default="", blank=True)

    class Meta:
        verbose_name = 'Chief'


class Program(models.Model):
    PROGRAM_TYPES = [('nac', 'Nacional'),
                     ('sec', 'Sectorial'),
                     ('ter', 'Territorial')]
    name = models.CharField(max_length=512)
    program_code = models.CharField(max_length=10, default="0")
    chief = models.OneToOneField(Chief,
                                 on_delete=models.CASCADE,
                                 related_name='program',
                                 null=True, blank=True)
    ptype = models.TextField(choices=PROGRAM_TYPES, default='nac')
    strategics_sectors = models.TextField(null=True, blank=True)
    entities = models.TextField(null=True, blank=True)
    main_entity = models.TextField(null=True, blank=True)
    secretary = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    money = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECTS_TYPES = [
        ('papn', 'Proyectos Asociados a Programas Nacional'),
        ('paps', 'Proyectos Asociados a Programas Sectorial'),
        ('papt', 'Proyectos Asociados a Programas Territorial'),
        ('pnap_pe', 'Proyectos No Asociados a Programas (PE)'),
        ('pnap_pne', 'Proyectos No Asociados a Programas (PNE)'),
        ('pnap_pdl', 'Proyectos No Asociados a Programas (PDL)'),
        ('pnap_prci', 'Proyectos No Asociados a Programas (PRCI)'),
        ('pnap_pi', 'Proyectos No Asociados a Programas (PI)')

    ]
    PROJECTS_CLASS_OPTIONS = [
        ('i_bas', 'De Investigación Básica'),
        ('i_d', 'Aplicada y de Desarrollo'),
        ('inn', 'Innovación')
    ]
    name = models.CharField(max_length=255)
    project_code = models.CharField(max_length=10, default="0")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    program_code = models.CharField(max_length=10, default="0", null=True, blank=True)
    project_classification = models.TextField(max_length=255, choices=PROJECTS_CLASS_OPTIONS, default='i_bas')
    pj_type = models.TextField(max_length=255, choices=PROJECTS_TYPES, default='papt')
    strategics_sectors = models.TextField(null=True, blank=True)
    main_entity = models.CharField(max_length=255)
    entities = models.TextField()
    chief = models.ForeignKey(Chief, on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    financing = models.PositiveBigIntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Member(models.Model):
    M_TYPES = [
        ('in', 'Interno'),
        ('out', 'Externo'),
        ('stdnt', 'Estudiante')
    ]
    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    c_id = models.CharField(max_length=11)
    organization = models.CharField(max_length=500, default='')
    projects = models.ManyToManyField(Project, related_name='members', blank=True)
    m_type = models.TextField(max_length=255, choices=M_TYPES, default='in')

    def __str__(self):
        return self.name


class Document(models.Model):
    file = models.FileField(upload_to=os.path.join('Documentación'), max_length=256)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectDocument(models.Model):

    def get_upload_folder(self, filename):
        program = self.project.program

        if program is not None:
            return os.path.join('Programas', program.name, 'Projectos', self.project.name, filename)
        else:
            return os.path.join('Projectos', self.project.name, filename)

    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='documents')
    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True, max_length=256)
    DOCUMENT_TYPES = [('other', 'Otro'),
                      ('profile', 'Perfil'),
                      ('contract', 'Contrato'),
                      ('rsjf', 'Resolución de nombramiento del jefe de proyecto'),
                      ('cidef', 'Compatibilización con los intereses de la Defensa'),
                      ('roap', 'Resolución oficial de aprobación del proyecto'),
                      ('dapp', 'Dictamen de aprobación del proyecto por el programa'),
                      ('dapcca', 'Dictamen de aprobación del proyecto por el CCA'),
                      ('dpddp', 'Documentos de planificación del diseño y desarrollo del producto'),
                      ('csbie', 'Certifico del salario básico de los investigadores externos'),
                      ('fciie', 'Fotos escaneadas del carné de identidad de los investigadores')]
    dtype = models.CharField(max_length=512, choices=DOCUMENT_TYPES, default='other')

    def __str__(self):
        return self.name if self.dtype == 'other' else self.get_dtype_display()


class DocumentGroup(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='document_groups')

    DOCUMENT_TYPES = [('other', 'Otro'),
                      ('dpac', 'Desglose del presupuesto del año en curso'),
                      ('mca', 'Anexo 15 Modelo de certificación de actividades'),
                      ('isp', 'Anexo 13 Informe semestral del proyecto'),
                      ('ict', 'Informe científico técnico'),
                      ('dapiscca', 'Dictamen de aprobación del informe semestral por el CCA'),
                      ('dgeri', 'Dictamen del Grupo de Expertos sobre los resultados y el Informe de la Etapa'),
                      ('mnig', 'Anexo 16 Modelo de Notificación de Ingresos/Gastos'),
                      ('bcpr', 'Base de cálculo para el pago por remuneración'),
                      ('acpp', 'Acta de conformidad de los participantes del proyecto'),
                      ('cpr', 'Certificación para el pago de la remuneración'),
                      ('cpie', 'Anexo 8. Certifico para el pago de los investigadores externos')]

    dtype = models.CharField(max_length=512, choices=DOCUMENT_TYPES, default='other')

    def __str__(self):
        return self.name if self.dtype == 'other' else self.get_dtype_display()


class GroupDocument(models.Model):

    def get_upload_folder(self, filename):
        program = self.group.project.program
        group = self.group.name if self.group.dtype == 'other' else self.group.get_dtype_display()

        if program is not None:
            return os.path.join('Programas', program.name, 'Projectos', self.group.project.name, group,
                                filename)
        else:
            return os.path.join('Projectos', self.group.project.name, group, filename)

    group = models.ForeignKey(DocumentGroup,
                              on_delete=models.CASCADE,
                              related_name='documents')

    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True, max_length=256)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.group.name + '_' + str(
            self.date) if self.group.dtype == 'other' else self.group.get_dtype_display() + '_' + str(self.date)


class ProgramDocument(models.Model):

    def get_upload_folder(self, filename):
        return os.path.join('Programas', self.program.name, filename)

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='documents', null=True)

    DOCUMENT_TYPES = [('other', 'Otro'),
                      ('profile', 'Perfil'),
                      ('contract', 'Contrato'),
                      ('rsjf', 'Resolución de nombramiento del equipo de dirección'),
                      ('dap', 'Documento de aprobación del programa'),
                      ('daeg', 'Documento de aprobación de la entidad gestora'),
                      ('cidef', 'Compatibilización con los intereses de la Defensa'),
                      ('dpddp', 'Documentos de planificación del diseño y desarrollo del producto'),
                      ('csbie', 'Certifico del salario básico de los investigadores externos'),
                      ('fciie', 'Fotos escaneadas del carné de identidad de los investigadores')]
    dtype = models.CharField(max_length=512, choices=DOCUMENT_TYPES, default='other')

    def __str__(self):
        return self.name if self.dtype == 'other' else self.get_dtype_display()


class ProgramDocumentGroup(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    program = models.ForeignKey(Program,
                                on_delete=models.CASCADE,
                                related_name='document_groups')

    DOCUMENT_TYPES = [('other', 'Otro'),
                      ('dpac', 'Desglose del presupuesto del año en curso'),
                      ('mca', 'Anexo 15 Modelo de certificación de actividades'),
                      ('rdlc', 'Resultados de la convocatoria'),
                      ('rpe', 'Relación de proyectos en ejecucion'),
                      ('arge', 'Actas de las reuniones del grupo de expertos'),
                      ('iar', 'Informe anual de resultados del programa'),
                      ('ifp', 'Informe final del programa'),
                      ('bcpr', 'Base de cálculo para el pago por remuneración'),
                      ('acpp', 'Acta de conformidad de los participantes del programa'),
                      ('cpr', 'Certificación para el pago de la remuneración'),
                      ('cpie', 'Anexo 8. Certifico para el pago de los investigadores externos')]

    dtype = models.CharField(max_length=512, choices=DOCUMENT_TYPES, default='other')

    def __str__(self):
        return self.name if self.dtype == 'other' else self.get_dtype_display()


class ProgramGroupDocument(models.Model):

    def get_upload_folder(self, filename):
        program = self.group.program
        group = self.group.name if self.group.dtype == 'other' else self.group.get_dtype_display()

        return os.path.join('Programas', program.name, group, filename)

    group = models.ForeignKey(ProgramDocumentGroup,
                              on_delete=models.CASCADE,
                              related_name='documents')

    file = models.FileField(upload_to=get_upload_folder, null=True, blank=True, max_length=256)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.group.name + '_' + str(
            self.date) if self.group.dtype == 'other' else self.group.get_dtype_display() + '_' + str(self.date)
