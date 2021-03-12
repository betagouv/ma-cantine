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

function findSubMeasure(id) {
  for (let measureIdx = 0; measureIdx < keyMeasures.length; measureIdx++) {
    const measure = keyMeasures[measureIdx];
    const subMeasure = measure.subMeasures.find((subMeasure) => subMeasure.id === id);
    if(subMeasure) { return subMeasure; }
  }
}

export {
  keyMeasures,
  saveStatus,
  findSubMeasure
};