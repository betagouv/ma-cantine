import keyMeasures from "@/data/key-measures.json";

let statuses = localStorage.getItem('statuses') || "{}";
statuses = JSON.parse(statuses);

keyMeasures.forEach(measure => {
  let score = 0;
  measure.subMeasures.forEach(subMeasure => {
    subMeasure.status = statuses[subMeasure.id];
    if(subMeasure.status === 'done') {
      score += 1;
    } else if(subMeasure.status === 'planned') {
      score += 0.5;
    }
  });
  measure.statusMaxScore = measure.subMeasures.length;
  measure.statusScore = score;
});

export default keyMeasures;