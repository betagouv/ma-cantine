import keyMeasures from "@/data/key-measures.json";

function saveStatus(id, status) {
  const statuses = JSON.parse(localStorage.getItem('statuses') || '{}');
  statuses[id] = status;
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
  saveStatus
};