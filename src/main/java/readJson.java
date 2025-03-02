import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class readJson {
    // Correctly mapping JSON structure
    public static Map<String, Map<String, PlayerData>> loadMockData() {
        Gson gson = new Gson();

        // Load file from classpath
        InputStream inputStream = readJson.class.getClassLoader().getResourceAsStream("mock_data.json");

        if (inputStream == null) {
            System.err.println("Error: mock_data.json file not found in resources!");
            return null;
        }

        try (InputStreamReader reader = new InputStreamReader(inputStream, StandardCharsets.UTF_8)) {
            Type mapType = new TypeToken<Map<String, Map<String, PlayerData>>>() {}.getType();
            return gson.fromJson(reader, mapType);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    // Correctly define a PlayerData class matching JSON structure
    public static class PlayerData {
        List<Integer> odd;  // This matches "odd": [150, 160]
        Float goal;       // This matches "goal": 2.5
    }
}
