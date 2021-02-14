import KeyMeasure from '@/components/KeyMeasure'
import keyMeasures from '@/data/key-measures.json'

export default {
  components: {
    KeyMeasure,
  },
  data() {
    return {
      keyMeasures,
    };
  }
}
