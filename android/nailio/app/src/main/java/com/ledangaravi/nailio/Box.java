package com.ledangaravi.nailio;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

public class Box extends View {
    private Paint paint = new Paint();
    Box(Context context) {
        super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) { // Override the onDraw() Method
        super.onDraw(canvas);

        paint.setStyle(Paint.Style.STROKE);
        paint.setColor(getResources().getColor(R.color.colorGreen));
        paint.setStrokeWidth(10);

        //center
        int x0 = getWidth()/2;
        int y0 = getHeight()/2;
        int dx = getWidth()/3;
        int dy = dx;//getHeight()/3;
        //draw guide box
        canvas.drawRect(x0-dx, y0-dy, x0+dx, y0+dy, paint);
    }
}