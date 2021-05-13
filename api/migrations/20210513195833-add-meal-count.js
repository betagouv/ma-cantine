'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return queryInterface.addColumn('canteens', 'mealCount', {
        type: Sequelize.DataTypes.INTEGER,
      }, { transaction: t });
    });
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return queryInterface.removeColumn('canteens', 'mealCount', { transaction: t });
    });
  }
};
