{#
    Référentiel des secteurs d'activité : code, libellé, libellé de la catégorie.

    Copie écrite à la main de `data/models/sector.py` (classes `Sector` et
    `SectorCategory`, listes `*_SECTOR_LIST` pour le rattachement secteur → catégorie).
    Ne jamais retirer un code : les anciennes TD l'utilisent encore.
    À remplacer par une source le jour où l'application exporte ces référentiels.

    Source unique des macros `libelles_secteurs` et `libelles_categories`.
    Le test `tests/assert_codes_secteurs_et_ministeres_ont_un_libelle.sql`
    signale tout code présent dans les données mais absent d'ici.
#}

{% macro referentiel_secteurs() %}
    (values
        ('administration_prison',                           'Restaurants des prisons',                                            'Administration'),
        ('administration_administratif',                    'Restaurants administratifs d''Etat (RA)',                            'Administration'),
        ('administration_armee',                            'Restaurants des armées / police / gendarmerie',                      'Administration'),
        ('administration_etablissement_public',             'Etablissements publics d''Etat (EPA ou EPIC)',                       'Administration'),
        ('administration_inter_administratif',              'Restaurants inter-administratifs d''État (RIA)',                     'Administration'),
        ('administration_administratif_des_collectivites',  'Restaurants administratifs des collectivités territoriales',         'Administration'),
        ('entreprise_entreprise',                           'Restaurants d''entreprises',                                         'Entreprise'),
        ('entreprise_inter_entreprise',                     'Restaurants inter-entreprises',                                      'Entreprise'),
        ('education_primaire',                              'Ecole primaire (maternelle et élémentaire)',                         'Enseignement'),
        ('education_secondaire_college',                    'Secondaire collège',                                                 'Enseignement'),
        ('education_secondaire_lycee',                      'Secondaire lycée (hors agricole)',                                   'Enseignement'),
        ('education_enseignement_agricole',                 'Etablissements d''enseignement agricole',                            'Enseignement'),
        ('education_superieur_universitaire',               'Supérieur et Universitaire',                                         'Enseignement'),
        ('education_autre',                                 'Autres structures d''enseignement',                                  'Enseignement'),
        ('sante_hopital',                                   'Hôpitaux',                                                           'Santé'),
        ('sante_clinique',                                  'Cliniques',                                                          'Santé'),
        ('sante_autre',                                     'Autres établissements de soins',                                     'Santé'),
        ('social_creche',                                   'Crèche',                                                             'Social / Médico-social'),
        ('social_ime',                                      'IME / ITEP',                                                         'Social / Médico-social'),
        ('social_esat',                                     'ESAT / Etablissements spécialisés',                                  'Social / Médico-social'),
        ('social_ehpad',                                    'EHPAD / maisons de retraite / foyers de personnes âgées',            'Social / Médico-social'),
        ('social_pjj',                                      'Etablissements de la PJJ',                                           'Social / Médico-social'),
        ('social_autre',                                    'Autres établissements sociaux et médico-sociaux',                    'Social / Médico-social'),
        ('loisir_centre_vacances',                          'Centre de vacances / sportif',                                       'Loisirs'),
        ('loisir_autre',                                    'Autres établissements de loisirs',                                   'Loisirs'),
        ('autres_autre',                                    'Autres établissements non listés',                                   'Autres')
    ) as referentiel_secteurs (code, libelle, libelle_categorie)
{% endmacro %}
