'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return Promise.all([
        queryInterface.addColumn('canteens', 'hasPublished', {
          type: Sequelize.DataTypes.BOOLEAN,
          defaultValue: false,
        }, { transaction: t }),
        queryInterface.addColumn('canteens', 'dataIsPublic', {
          type: Sequelize.DataTypes.BOOLEAN,
          defaultValue: false,
        }, { transaction: t })
      ]);
    });
  },

  down: async (queryInterface, Sequelize) => {
    return queryInterface.sequelize.transaction(t => {
      return Promise.all([
        queryInterface.removeColumn('canteens', 'hasPublished', { transaction: t }),
        queryInterface.removeColumn('canteens', 'dataIsPublic', { transaction: t })
      ]);
    });
  }
};
