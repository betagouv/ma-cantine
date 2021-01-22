import InfoCard from '@/views/KeyMeasuresPage/InfoCard'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

export default {
  components: {
    InfoCard
  },
  data() {
    return {
      keyMeasures,
      tags
    };
  }
}