<template>
  <v-simple-table class="my-6">
    <template v-slot:default>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Champ</th>
          <th>Description</th>
          <th>Type</th>
          <th>Exemple</th>
          <th>Obligatoire</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(field, idx) in schemaFieldList" :key="idx">
          <td>{{ field.name }}</td>
          <td>{{ field.title }}</td>
          <td>
            <p>{{ field.description }}</p>
            <p v-if="field.constraints && field.constraints.enum">
              <span>Options acceptées :&#32;</span>
              <span v-for="(item, idx) in field.constraints.enum" :key="idx">
                <code>{{ item }}</code>
                <span v-if="idx < field.constraints.enum.length - 1">,&#32;</span>
              </span>
              .
            </p>
            <p v-if="field.constraints && field.constraints.enum_multiple">
              Spécifiez plusieurs options en séparant avec un
              <code>{{ field.constraints.enum_multiple_seperator }}</code>
              .
            </p>
          </td>
          <td style="min-width: 150px;">{{ getSchemaFieldType(field) }}</td>
          <td>{{ field.example }}</td>
          <td class="text-center">{{ field.constraints && field.constraints.required ? "✔" : "✘" }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
const schemaTypes = {
  date: "Date (au format AAAA-MM-JJ)",
  integer: "Chiffre",
  number: "Chiffre",
  siret: "14 chiffres, avec ou sans espaces",
  string: "Texte",
  string_enum: "Texte (choix unique)",
  string_enum_multiple: "Texte (choix multiples)",
}

export default {
  props: {
    schemaUrl: String,
  },
  data() {
    return {
      schemaFieldList: [],
    }
  },
  mounted() {
    this.fetchSchema()
  },
  methods: {
    fetchSchema() {
      fetch(this.schemaUrl)
        .then((response) => response.json())
        .then((json) => {
          this.schemaFieldList = json.fields
        })
    },
    getSchemaFieldType(field) {
      if (field.name in schemaTypes) {
        return schemaTypes[field.name]
      }
      if (field.constraints && field.constraints.enum) {
        if (field.constraints.enum_multiple) {
          return schemaTypes[`${field.type}_enum_multiple`]
        }
        return schemaTypes[`${field.type}_enum`]
      }
      return schemaTypes[field.type]
    },
  },
}
</script>
