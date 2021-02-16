import keyMeasures from "@/data/key-measures.json";

let statuses = localStorage.getItem('statuses') || "{}";
statuses = JSON.parse(statuses);

keyMeasures.forEach(measure => {
  measure.subMeasures.forEach(subMeasure => {
    subMeasure.status = statuses[subMeasure.id];
  });
});

export default keyMeasures;