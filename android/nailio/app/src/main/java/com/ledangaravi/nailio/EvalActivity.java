package com.ledangaravi.nailio;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.widget.ImageView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;

public class EvalActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_eval);

        Intent intent = getIntent();
        String photoPath = intent.getStringExtra(CaptureActivity.EXTRA_MESSAGE);

        Bitmap bitmap = BitmapFactory.decodeFile(photoPath);
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();

        Bitmap croppedBmp = Bitmap.createBitmap(bitmap, width/6, height/2-width/3, width*2/3, width*2/3);

        ImageView imageView = findViewById(R.id.eval_image_view);
        imageView.setImageBitmap(croppedBmp);

        final String imageBase64 = convert(bitmap);

        RequestQueue queue = Volley.newRequestQueue(this);
        String url = "http://35.204.14.232:6065";

        final JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("Image",imageBase64);
            jsonBody.put("UID","0");

            // Request a string response from the provided URL.
            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            // your response
                            Log.d("myTag", response);

                        }
                    }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    // error
                    Log.d("myTag", error.getMessage());
                }
            }){
                @Override
                public byte[] getBody() throws AuthFailureError {
                    String your_string_json = jsonBody.toString(); // put your json
                    return your_string_json.getBytes();
                }
            };

            queue.add(stringRequest);
        }
        catch (JSONException e) {
            e.printStackTrace();
        }

    }



    public static String convert(Bitmap bitmap)
    {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream);

        return Base64.encodeToString(outputStream.toByteArray(), Base64.DEFAULT);
    }
}
