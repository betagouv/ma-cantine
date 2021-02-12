import InfoCard from '@/views/KeyMeasuresPage/InfoCard'
import KeyMeasureTitle from '@/components/KeyMeasureTitle'
import KeyMeasureDescription from '@/components/KeyMeasureDescription'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

export default {
  components: {
    InfoCard,
    KeyMeasureTitle,
    KeyMeasureDescription
  },
  data() {
    return {
      keyMeasures,
      tags
    };
  }
}