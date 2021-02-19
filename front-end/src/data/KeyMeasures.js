import keyMeasures from "@/data/key-measures.json";

function saveStatuses() {
  let statuses = {};
  keyMeasures.forEach((measure) => {
    measure.subMeasures.forEach((subMeasure) => {
      if(subMeasure.status) {
        statuses[subMeasure.id] = subMeasure.status;
      }
    });
  });
  localStorage.setItem('statuses', JSON.stringify(statuses));
}

const statusesString = localStorage.getItem('statuses') || "{}";
const statuses = JSON.parse(statusesString);

keyMeasures.forEach(measure => {
  measure.subMeasures.forEach(subMeasure => {
    subMeasure.status = statuses[subMeasure.id];
  });
});

export {
  keyMeasures,
  saveStatuses
};