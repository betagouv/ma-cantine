const { DataTypes } = require('sequelize');
const { sequelize } = require('../postgres-database');
const { User } = require('./user');

const EXPIRE_MINUTES = 60;
const MILLISECONDS_IN_MINUTE = 60000;

let LoginToken = sequelize.define('loginToken', {
  token: {
    type: DataTypes.STRING,
    primaryKey: true,
    unique: true,
    allowNull: false
  },
  expirationDate: {
    type: DataTypes.VIRTUAL,
    get() {
      const tokenCreated = new Date(this.createdAt);
      return new Date(tokenCreated.getTime() + (EXPIRE_MINUTES * MILLISECONDS_IN_MINUTE));
    }
  }
});

User.hasOne(LoginToken, {
  foreignKey: {
    allowNull: false
  }
});
LoginToken.belongsTo(User);

exports.LoginToken = LoginToken;