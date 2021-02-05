import InfoCard from '@/views/KeyMeasuresPage/InfoCard'
import KeyMeasureTitle from '@/components/KeyMeasureTitle'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

export default {
  components: {
    InfoCard,
    KeyMeasureTitle
  },
  data() {
    return {
      keyMeasures,
      tags
    };
  }
}