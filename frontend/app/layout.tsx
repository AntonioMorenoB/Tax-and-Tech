export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <head>
        <title>Tax and Technology AM</title>
        <link rel="stylesheet" href="/styles/globals.css" />
      </head>
      <body>{children}</body>
    </html>
  );
}