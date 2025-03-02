import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.*;

public class readJson {
    public static Map<String, Map<String, Map<String, List<Integer>>>> loadMockData(String filePath) {
        Gson gson = new Gson();
        try (FileReader reader = new FileReader(filePath)) {
            Type mapType = new TypeToken<Map<String, Map<String, Map<String, List<Integer>>>>>() {}.getType();
            return gson.fromJson(reader, mapType);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

}
