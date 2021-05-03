'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('diagnostics', {
      canteenId: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        allowNull: false,
        references: {
          model: 'canteens',
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE'
      },
      year: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        allowNull: false
      },
      valueBio: Sequelize.FLOAT,
      valueFairTrade: Sequelize.FLOAT,
      valueSustainable: Sequelize.FLOAT,
      valueTotal: Sequelize.FLOAT,
      hasMadeWasteDiagnostic: Sequelize.BOOLEAN,
      hasMadeWastePlan: Sequelize.BOOLEAN,
      wasteActions: Sequelize.ARRAY(Sequelize.STRING),
      hasDonationAgreement: Sequelize.BOOLEAN,
      hasMadeDiversificationPlan: Sequelize.BOOLEAN,
      vegetarianFrequency: Sequelize.STRING,
      vegetarianMenuType: Sequelize.STRING,
      cookingFoodContainersSubstituted: Sequelize.BOOLEAN,
      serviceFoodContainersSubstituted: Sequelize.BOOLEAN,
      waterBottlesSubstituted: Sequelize.BOOLEAN,
      disposableUtensilsSubstituted: Sequelize.BOOLEAN,
      communicationSupport: Sequelize.ARRAY(Sequelize.STRING),
      communicationSupportLink: Sequelize.STRING,
      communicateOnFoodPlan: Sequelize.BOOLEAN,
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('diagnostics');
  }
};
