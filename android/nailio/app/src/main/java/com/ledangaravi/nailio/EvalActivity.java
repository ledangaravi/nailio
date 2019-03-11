package com.ledangaravi.nailio;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.graphics.PorterDuffXfermode;
import android.graphics.Rect;
import android.graphics.RectF;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;

public class EvalActivity extends AppCompatActivity {
    public static String score;
    public static String diagnosis;
    public static String confidence;

    Bitmap croppedBmp;
    TextView tvTitle;
    TextView tvScore;
    TextView tvNailedIt;
    Button buttonMore;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_eval);
        tvTitle = findViewById(R.id.eval_nailio_score_title);
        tvScore = findViewById(R.id.eval_nailio_score);
        tvNailedIt = findViewById(R.id.eval_nailed_it);

        buttonMore = findViewById(R.id.eval_button_learn_more);

        final Intent intent = getIntent();
        String photoPath = intent.getStringExtra(CaptureActivity.EXTRA_MESSAGE);

        Bitmap bitmap = BitmapFactory.decodeFile(photoPath);
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();

        croppedBmp = Bitmap.createBitmap(bitmap, width/6, height/2-width/3, width*2/3, width*2/3);

        final ImageView imageView = findViewById(R.id.eval_image_view);
        Bitmap rounded = getRoundedCornerBitmap(croppedBmp, 20);
        imageView.setImageBitmap(rounded);


        final FloatingActionButton fabRedo = (FloatingActionButton) findViewById(R.id.eval_fab_redo);
        fabRedo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent1 = new Intent(getApplicationContext(), CaptureActivity.class);
                startActivity(intent1);
            }
        });

        final FloatingActionButton fabCheck = (FloatingActionButton) findViewById(R.id.eval_fab_check);
        fabCheck.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendImage();
                tvTitle.setVisibility(View.VISIBLE);
                tvScore.setVisibility(View.VISIBLE);
                fabCheck.hide();
                fabRedo.hide();
                imageView.setVisibility(View.INVISIBLE);

            }
        });


    }

    public void learnMore(View view){
        Intent intent = new Intent(this, Tips1Activity.class);
        startActivity(intent);
    }

    void sendImage(){
        final String imageBase64 = convert(croppedBmp);

        RequestQueue queue = Volley.newRequestQueue(this);
        String url = "http://35.204.92.147:6065";

        final JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("Image",imageBase64);
            jsonBody.put("UID","0");

            // Request a string response from the provided URL.
            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            Log.d("myTag", response);
                            try {
                                JSONObject data = new JSONObject(response.substring(response.indexOf('{')));
                                Log.d("myTag",response.substring(response.indexOf('{')));

                                //String normalNail = data.getString("normalnail");
                                //Log.d("myTag", normalNail);


                                buttonMore.setVisibility(View.VISIBLE);


                                score = data.getString("nailioscore");
                                diagnosis = data.getString("condition");
                                confidence = data.getString("confidence");
                                //score = "7";//data.getString("normalnail") + "/10";
                                //diagnosis = "normal";
                                //confidence = "90%";
                                tvScore.setText(score + "/10");
                                tvScore.setTextSize(96);

                                if(Integer.parseInt(score) >= 7){
                                    tvNailedIt.setVisibility(View.VISIBLE);
                                }


                            } catch (JSONException e) {
                                Log.d("myTag", e.getMessage());
                            }


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

            stringRequest.setRetryPolicy(new RetryPolicy() {
                @Override
                public int getCurrentTimeout() {
                    return 10000;
                }

                @Override
                public int getCurrentRetryCount() {
                    return 10000;
                }

                @Override
                public void retry(VolleyError error) throws VolleyError {

                }
            });

            queue.add(stringRequest);
        }
        catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public static Bitmap getRoundedCornerBitmap(Bitmap bitmap, int pixels) {
        Bitmap output = Bitmap.createBitmap(bitmap.getWidth(), bitmap
                .getHeight(), Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(output);

        final int color = 0xff424242;
        final Paint paint = new Paint();
        final Rect rect = new Rect(0, 0, bitmap.getWidth(), bitmap.getHeight());
        final RectF rectF = new RectF(rect);
        final float roundPx = pixels;

        paint.setAntiAlias(true);
        canvas.drawARGB(0, 0, 0, 0);
        paint.setColor(color);
        canvas.drawRoundRect(rectF, roundPx, roundPx, paint);

        paint.setXfermode(new PorterDuffXfermode(PorterDuff.Mode.SRC_IN));
        canvas.drawBitmap(bitmap, rect, rect, paint);

        return output;
    }



    public static String convert(Bitmap bitmap)
    {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream);

        return Base64.encodeToString(outputStream.toByteArray(), Base64.DEFAULT);
    }
}
