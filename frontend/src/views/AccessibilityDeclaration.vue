<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="font-weight-black my-6">Déclaration d'accessibilité</h1>
    <p>
      <span>Le ministère de l'agriculture et de l'alimentation</span>
      s’engage à rendre son service accessible, conformément à l’article 47 de la loi n° 2005-102 du 11 février 2005.
    </p>
    <p>
      Cette déclaration d’accessibilité s’applique à
      <span>ma cantine</span>
      .
    </p>
    <h2 class="my-6">État de conformité</h2>
    <p>
      <span>ma cantine</span>
      est
      <b>
        <span data-printfilter="lowercase">non conforme</span>
        avec le
        <span data-negate="">RGAA 4.1</span>
      </b>
      .
      <span><span>Le site n'a encore pas été audité.</span></span>
    </p>
    <h2 class="my-6">Contenus non accessibles</h2>
    <h3 class="my-2">Non conformité</h3>
    <p>
      Malgré nos efforts, certains contenus sont inaccessibles. Vous trouverez ci-dessous une liste des limitations
      connues et des solutions potentielles :
    </p>
    <ol class="technical-information accessibility-limitations">
      <li>
        <strong>La page d'accueil</strong>
        : La vidéo de présentation des enjeux de la restauration collective n’a pas de transcription. Vous pouvez nous
        contacter pour faire une requête pour une transcription.
      </li>
      <li>
        <strong>La page d'accueil</strong>
        : Le livret de la loi EGAlim concernant la restauration collective est donné en format PDF sans alternatif. Vous
        pouvez nous contacter pour faire une requête pour un format alternatif.
      </li>
      <li>
        <strong>Le chatbox</strong>
        : Le chatbox n'est pas accessible par clavier. Nous offrons plusieurs mêthodes de contact (email, je donne mon
        avis).
      </li>
    </ol>
    <h2 class="my-6">Établissement de cette déclaration d'accessibilité</h2>
    <p>
      Cette déclaration a été établie le
      <b><span>23 août 2021</span></b>
      .
    </p>
    <h3 class="my-2">Technologies utilisées</h3>
    <p>
      L'accessibilité de
      <span>ma cantine</span>
      s'appuie sur les technologies suivantes :
    </p>
    <ul class="technical-information technologies-used">
      <li>HTML</li>
      <li>WAI-ARIA</li>
      <li>JavaScript</li>
    </ul>
    <h2 class="my-6">Amélioration et contact</h2>
    <p>
      Si vous n’arrivez pas à accéder à un contenu ou à un service, vous pouvez contacter le responsable de
      <span>ma cantine</span>
      pour être orienté vers une alternative accessible ou obtenir le contenu sous une autre forme.
    </p>
    <ul class="basic-information feedback h-card">
      <li>
        Téléphone :
        <span>+33 6 59 63 44 43</span>
      </li>
      <li>
        E-mail :
        <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
      </li>
      <li>
        Adresse :
        <span>20 avenue de Ségur, 75007, Paris</span>
      </li>
      <li>
        Twitter :
        <a href="https://twitter.com/egalimbetagouv">@egalimBetaGouv</a>
      </li>
    </ul>
    <p>
      Nous essayons de répondre dans les
      <span>2 jours ouvrés</span>
      .
    </p>
    <h2 class="my-6">Voie de recours</h2>
    <p>
      Cette procédure est à utiliser dans le cas suivant : vous avez signalé au responsable du site internet un défaut
      d’accessibilité qui vous empêche d’accéder à un contenu ou à un des services du portail et vous n’avez pas obtenu
      de réponse satisfaisante.
    </p>
    <p>Vous pouvez :</p>
    <ul>
      <li>
        Écrire un message au
        <a href="https://formulaire.defenseurdesdroits.fr/">Défenseur des droits</a>
      </li>
      <li>
        Contacter
        <a href="https://www.defenseurdesdroits.fr/saisir/delegues">
          le délégué du Défenseur des droits dans votre région
        </a>
      </li>
      <li>
        Envoyer un courrier par la poste (gratuit, ne pas mettre de timbre) :
        <br />
        Défenseur des droits
        <br />
        Libre réponse 71120 75342 Paris CEDEX 07
      </li>
    </ul>
    <v-divider class="my-4"></v-divider>
    <p>
      Cette déclaration d'accessibilité a été créé le
      <span>23 août 2021</span>
      grâce au
      <a href="https://betagouv.github.io/a11y-generateur-declaration/#create">
        Générateur de Déclaration d'Accessibilité de BetaGouv
      </a>
      .
    </p>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "AccessibilityDeclaration",
  components: { BreadcrumbsNav },
}
</script>
