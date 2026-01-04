/**
 * Task 2.2: MongoDB Implementation
 */

const { MongoClient } = require("mongodb");
const fs = require("fs");
const path = require("path");

const MONGO_URI = "mongodb://127.0.0.1:27017";
const DB_NAME = "fleximart";
const COLLECTION = "products";

async function main() {
  const client = new MongoClient(MONGO_URI);

  try {
    await client.connect();
    console.log("Connected to MongoDB");

    const db = client.db(DB_NAME);
    const products = db.collection(COLLECTION);


  // -----------------------------
  // Operation 1: Load Data (1 mark)
  // Import the provided JSON file into collection 'products'
  // -----------------------------

    const filePath = path.join(__dirname, "products_catalog.json");
    const jsonData = JSON.parse(fs.readFileSync(filePath, "utf-8"));

    // reset collection so results are consistent
    await products.deleteMany({});
    await products.insertMany(jsonData);
    console.log(` Operation 1: Inserted ${jsonData.length} products into '${COLLECTION}'`);

  //-------------------------------
  // Operation 2: Basic Query (2 marks)
  // Find all products in "Electronics" category with price less than 50000
  // Return only: name, price, stock
  //-------------------------------

  const op2 = await products
      .find({ category: "Electronics", price: { $lt: 50000 } })
      .project({ _id: 0, name: 1, price: 1, stock: 1 })
      .toArray();

    console.log("\n Operation 2: Electronics products < 50000 (name, price, stock)");
    console.table(op2);

    // -----------------------------
    // Operation 3: Review Analysis (2 marks)
    // Find all products that have average rating >= 4.0
    // Use aggregation to calculate average from reviews array
    // -----------------------------

    const op3 = await products
      .aggregate([
        { $unwind: "$reviews" },
        {
          $group: {
            _id: "$product_id",
            name: { $first: "$name" },
            category: { $first: "$category" },
            avg_rating: { $avg: "$reviews.rating" },
            review_count: { $sum: 1 },
          },
        },
        { $match: { avg_rating: { $gte: 4.0 } } },
        {
          $project: {
            _id: 0,
            product_id: "$_id",
            name: 1,
            category: 1,
            avg_rating: { $round: ["$avg_rating", 2] },
            review_count: 1,
          },
        },
        { $sort: { avg_rating: -1 } },
      ])
      .toArray();

    console.log("\n Operation 3: Products with avg rating >= 4.0");
    console.table(op3);

    // -----------------------------
    // Operation 4: Update Operation (2 marks)
    // Add a new review to product "ELEC001"
    // Review: { user: "U999", rating: 4, comment: "Good value", date: ISODate() }
    // -----------------------------

    const newReview = {
      user: "U999",
      rating: 4,
      comment: "Good value",
      date: new Date(), 
      
    };

    const op4 = await products.updateOne(
      { product_id: "ELEC001" },
      { $push: { reviews: newReview } }
    );

    console.log("\n Operation 4: Added new review to ELEC001");
    console.log("Matched:", op4.matchedCount, "Modified:", op4.modifiedCount);

    // -----------------------------
    // Operation 5: Complex Aggregation (3 marks)
    // Calculate average price by category
    // Return: category, avg_price, product_count
    // Sort by avg_price descending
    // -----------------------------
    const op5 = await products
      .aggregate([
        {
          $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 },
          },
        },
        {
          $project: {
            _id: 0,
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1,
          },
        },
        { $sort: { avg_price: -1 } },
      ])
      .toArray();

    console.log("\n Operation 5: Avg price by category");
    console.table(op5);

    console.log("\n All operations completed!");
    } catch (err) {
    console.error(" Error:", err.message);
  } finally {
    await client.close();
    console.log(" Disconnected");
  }
}  
main();