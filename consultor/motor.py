"""25 regras SE-ENTÃO, executadas pelo encadeamento para frente do Experta.

A adaptação de Mapping é local ao processo: frozendict 1.2, exigido por
Experta 1.9.4, usa o nome removido de collections no Python 3.10.
"""
import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import Fact, Field, KnowledgeEngine, Rule, L, MATCH

class Perfil(Fact):
    matematica = Field(str, mandatory=True)
    atividade = Field(str, mandatory=True)
    ferramenta = Field(str, mandatory=True)
    entrega = Field(str, mandatory=True)
    objetivo = Field(str, mandatory=True)

class Projeto(Fact):
    area = Field(str, mandatory=True)

class Evidencia(Fact):
    regra = Field(str, mandatory=True)
    carreira = Field(str, mandatory=True)
    pontos = Field(int, mandatory=True)
    motivo = Field(str, mandatory=True)

class MotorCarreiras(KnowledgeEngine):
    def apoiar(self, regra, carreira, pontos, motivo):
        self.declare(Evidencia(regra=regra, carreira=carreira, pontos=pontos, motivo=motivo))

    @Rule(Perfil(atividade=L('logica'), entrega='servicos'))
    def r01(self):
        self.apoiar('R01', 'backend', 8, 'Você combina interesse em algoritmos e regras de negócio com a entrega de serviços e APIs.')

    @Rule(Perfil(atividade=L('visual'), entrega='interface'))
    def r02(self):
        self.apoiar('R02', 'frontend', 8, 'Você combina interesse em layouts e experiências visuais com a entrega de interfaces web.')

    @Rule(Perfil(atividade=L('dados'), entrega='previsoes', matematica=L('media') | L('alta')))
    def r03(self):
        self.apoiar('R03', 'ciencia', 8, 'Você combina interesse em análise de dados com a entrega de previsões e modelos de IA. Sua afinidade matemática é média ou alta.')

    @Rule(Perfil(atividade=L('pipelines') | L('dados'), entrega='infra_dados'))
    def r04(self):
        self.apoiar('R04', 'engenharia', 8, 'Você combina interesse em integração de dados ou análise de dados com a entrega de infraestrutura de dados.')

    @Rule(Perfil(atividade=L('seguranca'), entrega='protecao'))
    def r05(self):
        self.apoiar('R05', 'seguranca', 8, 'Você combina interesse em proteção de sistemas com a entrega de proteção contra ataques.')

    @Rule(Perfil(atividade=L('automacao') | L('arquitetura'), entrega='operacao'))
    def r06(self):
        self.apoiar('R06', 'devops', 8, 'Você combina interesse em automação de deploys ou arquitetura de infraestrutura com a entrega de serviços disponíveis e deploys confiáveis.')

    @Rule(Perfil(atividade=L('arquitetura'), entrega='infraestrutura'))
    def r07(self):
        self.apoiar('R07', 'cloud', 8, 'Você combina interesse em arquitetura de infraestrutura com a entrega de infraestrutura escalável.')

    @Rule(Perfil(atividade=L('apps') | L('visual'), entrega='aplicativo'))
    def r08(self):
        self.apoiar('R08', 'mobile', 8, 'Você combina interesse em aplicativos móveis ou layouts e experiências visuais com a entrega de aplicativos para celulares.')

    @Rule(Perfil(atividade=L('testes') | L('logica'), entrega='qualidade'))
    def r09(self):
        self.apoiar('R09', 'qa', 8, 'Você combina interesse em investigação de falhas ou algoritmos e regras de negócio com a entrega de qualidade de software.')

    @Rule(Perfil(atividade=L('negocio'), entrega='produto'))
    def r10(self):
        self.apoiar('R10', 'produto', 8, 'Você combina interesse em necessidades de negócio com a entrega de prioridades de produto.')

    @Rule(Perfil(atividade=L('logica'), ferramenta=L('python') | L('java')))
    def r11(self):
        self.apoiar('R11', 'backend', 4, 'O interesse em algoritmos e regras de negócio combina com sua familiaridade em python ou java.')

    @Rule(Perfil(atividade=L('visual'), ferramenta=L('javascript') | L('design')))
    def r12(self):
        self.apoiar('R12', 'frontend', 4, 'O interesse em layouts e experiências visuais combina com sua familiaridade em javascript ou design.')

    @Rule(Perfil(atividade=L('dados'), ferramenta=L('python') | L('estatistica'), matematica=L('media') | L('alta')))
    def r13(self):
        self.apoiar('R13', 'ciencia', 4, 'O interesse em análise de dados combina com sua familiaridade em python ou estatistica.')

    @Rule(Perfil(atividade=L('pipelines') | L('dados'), ferramenta=L('python') | L('sql')))
    def r14(self):
        self.apoiar('R14', 'engenharia', 4, 'O interesse em integração de dados ou análise de dados combina com sua familiaridade em python ou sql.')

    @Rule(Perfil(atividade=L('seguranca'), ferramenta=L('linux') | L('seguranca')))
    def r15(self):
        self.apoiar('R15', 'seguranca', 4, 'O interesse em proteção de sistemas combina com sua familiaridade em linux ou seguranca.')

    @Rule(Perfil(atividade=L('automacao') | L('arquitetura'), ferramenta=L('linux') | L('containers')))
    def r16(self):
        self.apoiar('R16', 'devops', 4, 'O interesse em automação de deploys ou arquitetura de infraestrutura combina com sua familiaridade em linux ou containers.')

    @Rule(Perfil(atividade=L('arquitetura'), ferramenta=L('cloud') | L('linux')))
    def r17(self):
        self.apoiar('R17', 'cloud', 4, 'O interesse em arquitetura de infraestrutura combina com sua familiaridade em cloud ou linux.')

    @Rule(Perfil(atividade=L('apps') | L('visual'), ferramenta=L('mobile') | L('javascript')))
    def r18(self):
        self.apoiar('R18', 'mobile', 4, 'O interesse em aplicativos móveis ou layouts e experiências visuais combina com sua familiaridade em mobile ou javascript.')

    @Rule(Perfil(atividade=L('testes') | L('logica'), ferramenta=L('testes') | L('python')))
    def r19(self):
        self.apoiar('R19', 'qa', 4, 'O interesse em investigação de falhas ou algoritmos e regras de negócio combina com sua familiaridade em testes ou python.')

    @Rule(Perfil(atividade=L('negocio'), ferramenta=L('gestao') | L('design')))
    def r20(self):
        self.apoiar('R20', 'produto', 4, 'O interesse em necessidades de negócio combina com sua familiaridade em gestao ou design.')

    @Rule(Projeto(area=MATCH.area & (L('ciencia') | L('engenharia'))))
    def r21(self, area):
        self.apoiar('R21', area, 20, 'Você escolheu explicitamente o projeto desta trilha para experimentar.')

    @Rule(Projeto(area=MATCH.area & (L('devops') | L('cloud'))))
    def r22(self, area):
        self.apoiar('R22', area, 20, 'Você escolheu explicitamente o projeto desta trilha para experimentar.')

    @Rule(Projeto(area=MATCH.area & (L('frontend') | L('mobile'))))
    def r23(self, area):
        self.apoiar('R23', area, 20, 'Você escolheu explicitamente o projeto desta trilha para experimentar.')

    @Rule(Projeto(area=MATCH.area & (L('backend') | L('qa'))))
    def r24(self, area):
        self.apoiar('R24', area, 20, 'Você escolheu explicitamente o projeto desta trilha para experimentar.')

    @Rule(Projeto(area=MATCH.area & (L('seguranca') | L('produto'))))
    def r25(self, area):
        self.apoiar('R25', area, 20, 'Você escolheu explicitamente o projeto desta trilha para experimentar.')
