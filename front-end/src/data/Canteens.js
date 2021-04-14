import canteens from "@/data/canteens.json";

function getCanteenById(id) {
  return canteens.find(canteen => canteen.id === id);
}

export {
  getCanteenById,
};
