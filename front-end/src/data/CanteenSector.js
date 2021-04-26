function getCanteenSector() {
  return localStorage.getItem('sector') || "scolaire";
}

function saveCanteenSector(sector) {
  return localStorage.setItem('sector', sector);
}

export {
  getCanteenSector,
  saveCanteenSector,
};
