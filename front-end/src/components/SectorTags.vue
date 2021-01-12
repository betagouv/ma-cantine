<template>
  <div class="tags" v-if="tags">
    <p class="tag" :class="tag" v-for="tag in tags" :key="tag">
      {{ tagsInfo[tag] }}
    </p>
  </div>
</template>

<script>
const tagsInfo = {
  scolaire: "Scolaire",
  administration: "Administration",
  universitaire: "Universitaire",
  medical: "Médical",
  social: "Social",
  creche: "Crèche",
  loisirs: "Loisirs",
  entreprises: "Entreprises"
};

export default {
  name: "SectorTags",
  props: {
    tags: Array
  },
  data() {
    return {
      tagsInfo: tagsInfo,
    };
  },
};
</script>

<style scoped>
.tags {
  display: flex;
}

.tag {
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  text-align: center;
  line-height: 20px;

  border-radius: 50px;
  padding: 0 1em;
  margin: 0 0.3em;
}

.scolaire {
  background-color: #eb5c2e;
}

.administration {
  background-color: rgba(255, 82, 82, 0.28);
}

.universitaire {
  background-color: rgba(57, 107, 200, 0.42);
}

.medical {
  background-color: rgba(235, 92, 46, 0.56);
}

.social {
  background-color: rgba(150, 93, 123, 0.46);
}

.creche {
  background-color: rgba(249, 168, 38, 0.31);
}

.loisirs {
  background-color: rgba(159, 97, 106, 1);
}

.entreprises {
  background-color: rgba(57, 107, 200, 1);
}
</style>