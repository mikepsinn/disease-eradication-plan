// Cloudflare Worker to submit referendum votes
// Keeps Airtable API key secret on the edge

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    try {
      // Parse the incoming vote data
      const { fullName, email, country, referralCode } = await request.json();

      // Basic validation
      if (!fullName || !email || !country) {
        return new Response(JSON.stringify({ error: 'Missing required fields' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return new Response(JSON.stringify({ error: 'Invalid email format' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Get Airtable credentials from environment variables
      const AIRTABLE_API_KEY = env.AIRTABLE_API_KEY;
      const BASE_ID = env.AIRTABLE_BASE_ID;

      if (!AIRTABLE_API_KEY || !BASE_ID) {
        console.error('Missing Airtable credentials');
        return new Response(JSON.stringify({ error: 'Server configuration error' }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Step 1: Create Personnel record
      const personnelResponse = await fetch(
        `https://api.airtable.com/v0/${BASE_ID}/Personnel%20Roster`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fields: {
              'Full Name': fullName,
              'Email': email,
              'Status': 'Prospect'
            }
          })
        }
      );

      if (!personnelResponse.ok) {
        const error = await personnelResponse.text();
        console.error('Airtable Personnel error:', error);
        return new Response(JSON.stringify({ error: 'Failed to create personnel record' }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      const personnelData = await personnelResponse.json();
      const personnelId = personnelData.id;

      // Step 2: Create referendum vote
      const voteData = {
        fields: {
          'Country': country,
          'Date Voted': new Date().toISOString().split('T')[0], // YYYY-MM-DD
          'Verification Status': 'Pending',
          'Reward Tier': 'Tier 3',
          'Voter': [personnelId] // Link to personnel record
        }
      };

      // Add referral code if provided (as note for now)
      if (referralCode) {
        voteData.fields['Referral Code'] = referralCode;
      }

      const voteResponse = await fetch(
        `https://api.airtable.com/v0/${BASE_ID}/Global%20Referendum`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(voteData)
        }
      );

      if (!voteResponse.ok) {
        const error = await voteResponse.text();
        console.error('Airtable Vote error:', error);
        return new Response(JSON.stringify({ error: 'Failed to record vote' }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      const voteRecord = await voteResponse.json();

      // Generate referral code for this voter
      const refCode = `REF_${voteRecord.id.substring(0, 8)}`;

      // Return success with referral code
      return new Response(JSON.stringify({
        success: true,
        message: 'Vote recorded successfully',
        referralCode: refCode,
        voterId: voteRecord.id
      }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      });

    } catch (error) {
      console.error('Error processing vote:', error);
      return new Response(JSON.stringify({
        error: 'Internal server error',
        message: error.message
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      });
    }
  }
};
