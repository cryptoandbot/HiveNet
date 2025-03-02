import java.util.*;

public class MainApp {
    public static void main(String[] args) {
        // Load mock data from JSON
        Map<String, Map<String, readJson.PlayerData>> mockData = readJson.loadMockData();

        // Directly pass the full JSON data to EVCalc (it will extract subfields itself)
        if (mockData != null) {
            EVCalc.calculatePerWebsite(mockData);
        } else {
            System.out.println("Failed to load mock data.");
        }
    }
}
