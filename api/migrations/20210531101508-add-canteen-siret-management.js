'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return Promise.all([
        queryInterface.addColumn('canteens', 'siret', {
          type: Sequelize.DataTypes.STRING,
        }, { transaction: t }),
        queryInterface.addColumn('canteens', 'managementType', {
          type: Sequelize.DataTypes.STRING,
        }, { transaction: t })
      ]);
    });
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return Promise.all([
        queryInterface.removeColumn('canteens', 'siret', { transaction: t }),
        queryInterface.removeColumn('canteens', 'managementType', { transaction: t })
      ]);
    });
  }
};
